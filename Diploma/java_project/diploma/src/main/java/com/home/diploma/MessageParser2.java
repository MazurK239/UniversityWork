package com.home.diploma;

import java.nio.ByteBuffer;
import java.util.Arrays;

import javax.xml.bind.DatatypeConverter;

public class MessageParser2 {

public static boolean startUp = true;
	
	private static byte[] currentMessage = new byte[100];
	private static int pos = 0;
	private static int idx = 0;
	
	private static Object[][] satelliteInfo = new Object[12][2]; 
	
	private static int GPSWeek = 0;
	private static double timeInMessage;
	private static double pseudorange;


	public static void processByte(byte[] buffer) {
		for (int i=0; i<buffer.length; i++) {
			currentMessage[pos+i] = buffer[i];
			if (buffer[i] == (byte)179) {
				if (currentMessage[pos + i - 1] == (byte)176) {
					processMesage(Arrays.copyOfRange(currentMessage, 0, pos+i+1));
					pos = -i-1;
				}
			}
		}
		pos += buffer.length;
	}

	private static void processMesage(byte[] message) {
		byte messageType = message[4];
		
		if (startUp) {
			if ((messageType == (byte)11) && (message[5] == (byte)166)) {
				startUp = false;
				System.out.println("Let's go!");
			}
		} else {
			switch (messageType) {
			case (byte) 6:
				System.out.println("Version of Sirf is: "
						+ new String(Arrays.copyOfRange(message, 5, message.length - 4)));
				break;
			case (byte) 7:
				GPSWeek = ByteBuffer.wrap(message, 5, 2).getShort();
				DateClass.calculateRealDate(GPSWeek);
				MainWorkFlow.startAction();
				break;
			case (byte) 28:
				try {
					processNavMessage(message);
				} catch (ArrayIndexOutOfBoundsException e) {
					System.out.println("Exception at: " + DateClass.getDateString());
					System.out.println("In message " + DatatypeConverter.printHexBinary(message));
				}
				break;

			default:
				break;
			} 
		}
	}
	
	private static void processNavMessage(byte[] message) throws ArrayIndexOutOfBoundsException {
		byte[] tmp =  new byte[8];
		
		for (int i = 0; i < 4; i++) { // reorganizing bytes to get GPS software time 
			tmp[i] = message[15 + i];
			tmp[4+i] = message[11 + i];			
		}
		timeInMessage = ByteBuffer.wrap(tmp).getDouble();
			
		if (DateClass.isDifferentTime(timeInMessage)) { // begin new block of data in RINEX file if the time has changed
			
			if ((int)(timeInMessage)%86400 == 0) {        // start of a new day - calculate the new date and create a new file
				if((int)(timeInMessage) == 0) {DateClass.calculateRealDate(++GPSWeek);} // start of a new week
				DateClass.updateDay();
				DateClass.calculateRealTime(timeInMessage);
				RinexManipulator.createNewFile("./home" + DateClass.getYear() + DateClass.getMonth() + DateClass.getDay() + ".rinex");
			} else {				
				DateClass.calculateRealTime(timeInMessage);
			}
			
			String satellites = "";
			for (int i=0; i<idx; i++) {
				satellites += (String)satelliteInfo[i][0];
			}
			if (idx!=0) {  // don't send fist block (empty on startup)
				ServerConnector.addLine("\n" + satellites);
				DateClass.sendDateString();
			}
			
			String satLine;
			for (int i=0; i<idx; i++) {
				pseudorange = (double)satelliteInfo[i][1];		
				satLine = (String)satelliteInfo[i][0] + "   " + String.format("%.3f", pseudorange) + "\n";
				ServerConnector.addLine(satLine);
			}
			idx = 0;
		}

		satelliteInfo[idx][0] = message[10] < 10 ? "G0" + message[10] : "G" + message[10]; // satID

		for (int i = 0; i < 4; i++) { // reorganizing bytes to get pseudorange 
			tmp[i] = message[23 + i];
			tmp[4+i] = message[19 + i];			
		}
		satelliteInfo[idx][1] = ByteBuffer.wrap(tmp).getDouble(); // pseudorange
		
		idx += 1;

	}
	
}
