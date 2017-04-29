package com.home.diploma;

import java.nio.ByteBuffer;
import java.util.Arrays;

import javax.xml.bind.DatatypeConverter;

public class MessageParser1 {
public static boolean startUp = true;
	
	private static byte[] currentMessage = new byte[100];
	private static int pos = 0;
	private static int idx = 0;
	
	private static Object[][] satelliteInfo = new Object[12][2]; 
	
	private static int GPSWeek = 0;
	private static double clockBias = 0;
	private static double timeInMessage;
	private static double pseudorange;
	public static final double L1 = 1575420000.0; // L1 frequency in Hz
	public static final int SOL = 299792458; // Speed of Light (m/s)


	public static void processByte(byte[] buffer) {
		for (int i=0; i<buffer.length; i++) {
			currentMessage[pos+i] = buffer[i];
			if (buffer[i] == (byte)179) {
				if (currentMessage[pos + i - 1] == (byte)176) {
					processMessage(Arrays.copyOfRange(currentMessage, 0, pos+i+1));
					pos = -i-1;
				}
			}
		}
		pos += buffer.length;
	}

	private static void processMessage(byte[] message) {
		byte messageType = message[4];
		
		if (startUp) {
			if ((messageType == (byte)11) && (message[5] == (byte)166)) {
				startUp = false;
				System.out.println("Let's go!");
				MainWorkFlow.startAction();
			}
		} else {
			switch (messageType) {
			case (byte) 6:
				System.out.println("Version of Sirf is: "
						+ new String(Arrays.copyOfRange(message, 5, message.length - 4)));
				break;
			case (byte) 7:
				writeToFile(message);
				break;
			case (byte) 28:
				try {
					processMessage28(message);
				} catch (ArrayIndexOutOfBoundsException e) {
					System.out.println("Exception at: " + DateClass.getDateString());
					System.out.println("In message " + DatatypeConverter.printHexBinary(message));
					e.printStackTrace();
				}
				break;

			default:
				break;
			} 
		}
	}

	public static void processMessage28(byte[] message) throws ArrayIndexOutOfBoundsException {
		byte[] tmp =  new byte[8];
		
		satelliteInfo[idx][0] = message[10] < 10 ? "G0" + message[10] : "G" + message[10];
		for (int i = 0; i < 4; i++) { // reorganizing bytes to get GPS software time 
			tmp[i] = message[15 + i];
			tmp[4+i] = message[11 + i];			
		}
		timeInMessage = ByteBuffer.wrap(tmp).getDouble();
		
		for (int i = 0; i < 4; i++) { // reorganizing bytes to get pseudorange 
			tmp[i] = message[23 + i];
			tmp[4+i] = message[19 + i];			
		}
		satelliteInfo[idx][1] = ByteBuffer.wrap(tmp).getDouble();
		
		idx += 1;
	}
	
	private static void writeToFile(byte[] message) {
		GPSWeek = ByteBuffer.wrap(message, 5, 2).getShort();
		DateClass.calculateRealDate(GPSWeek);
	    clockBias = ByteBuffer.wrap(message, 16, 4).getInt() * 0.000000001; // nanoseconds -> seconds
		double time = (double)Math.round(timeInMessage - clockBias);
	    
	    String satellites = "";
	    for (int i=0; i<idx; i++) {
	    	satellites += (String)satelliteInfo[i][0];
	    }
		
		if ((int)(time)%86400 <= MainWorkFlow.messagePeriod - 1) {        // start of a new day - calculate the new date and create a new file
			DateClass.updateDay();
			DateClass.calculateRealTime(time);
			RinexManipulator.createNewFile("./home" + DateClass.getYear() + DateClass.getMonth() + DateClass.getDay() + ".rinex");
		} else {				
			DateClass.calculateRealTime(time);
		}
		RinexManipulator.addLine("\n" + satellites);
		DateClass.sendDateString();
		
		String satLine;
		for (int i=0; i<idx; i++) {
			pseudorange = (double)satelliteInfo[i][1] - clockBias  * SOL; // corrected for clock bias			
			satLine = (String)satelliteInfo[i][0] + "   " + String.format("%.3f", pseudorange) + "\n";
			RinexManipulator.addLine(satLine);
		}
		idx = 0;
	}
	

}
