package com.home.diploma;

import java.util.Arrays;
import java.nio.ByteBuffer;

import javax.xml.bind.DatatypeConverter;

public class MessageParser {

	public static boolean startUp = true;
	
	private static byte[] currentMessage = new byte[100];
	private static int pos = 0;
	
	private static int GPSWeek = 0;
	private static double clockBias = 0;
	private static int clockDrift = 0;
	public static final double L1 = 1575420000.0; // L1 frequency in Hz
	public static final int SOL = 299792458; // Speed of Light (m/s)


	public static void processByte(byte[] buffer) {
		for (int i=0; i<buffer.length; i++) {
			currentMessage[pos+i] = buffer[i];
			if (buffer[i] == (byte)179) {
				if (currentMessage[pos + i - 1] == (byte)176) {
					processMesage(Arrays.copyOfRange(currentMessage, 0, pos+i+1));
//					System.out.println(DatatypeConverter.printHexBinary(Arrays.copyOfRange(currentMessage, 0, pos+i+1)));
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
			    clockBias = ByteBuffer.wrap(message, 16, 4).getInt() * 0.000000001; // nanoseconds -> seconds
			    clockDrift = ByteBuffer.wrap(message, 12, 4).getInt(); // Hz
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
		int satID = message[10];
		
		for (int i = 0; i < 4; i++) { // reorganizing bytes to get GPS software time 
			tmp[i] = message[15 + i];
			tmp[4+i] = message[11 + i];			
		}
		double timeInMessage = ByteBuffer.wrap(tmp).getDouble();
	
		if (DateClass.isDifferentTime(timeInMessage)) { // begin new block of data in RINEX file if the time has changed
			if ((int)(timeInMessage - clockBias)%86400 == 0) {        // start of a new day - calculate the new date and create a new file
				DateClass.updateDay();
				DateClass.calculateRealTime(timeInMessage - clockBias);
				RinexManipulator.createNewFile("./home" + DateClass.getYear() + DateClass.getMonth() + DateClass.getDay() + ".rinex");
			} else {				
				DateClass.calculateRealTime(timeInMessage - clockBias);
			}
			clockBias += (clockDrift/L1); // updated the clock bias with the known Change in Clock Bias (s/s) MainWorkFlow.messagePeriod * 
			DateClass.sendDateString();
		}
		
		for (int i = 0; i < 4; i++) { // reorganizing bytes to get pseudorange 
			tmp[i] = message[23 + i];
			tmp[4+i] = message[19 + i];			
		}
		double pseudorange = ByteBuffer.wrap(tmp).getDouble() - clockBias  * SOL; // corrected for clock bias
		
		String prefix;
		if (satID < 10) {prefix = "G0";} else {prefix = "G";}
		String satLine = prefix + satID + "   " + String.format("%.3f", pseudorange) + "\n";
		RinexManipulator.addLine(satLine);
	}
	
	
}
