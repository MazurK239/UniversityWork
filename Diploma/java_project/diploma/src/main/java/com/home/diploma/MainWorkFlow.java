package com.home.diploma;

import java.io.File;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.util.Scanner;

import javax.xml.bind.DatatypeConverter;

import com.home.diploma.EventListener;

import jssc.SerialPort;
import jssc.SerialPortException;

public class MainWorkFlow {

	public static String pollClock = "A0A2000290000090B0B3";
	public static String pollVersion = "A0A2000284000084B0B3";
	public static String disableAllMessages = "A0A20008A6021C000000000000C4B0B3";
	public static String disableMessage28 = "A0A20008A6001C000000000000C2B0B3";
	public static String setMessage28_1 = "A0A20008A6001C010000000000C3B0B3";
	public static String setMessage28_2 = "A0A20008A6001C020000000000C4B0B3";
	public static String setMessage28_5 = "A0A20008A6001C050000000000C7B0B3";
	public static String getClockMessage_1 = "A0A20008A60007010000000000AEB0B3";
	public static String getClockMessage_2 = "A0A20008A60007020000000000AFB0B3";
	public static String getClockMessage_5 = "A0A20008A60007050000000000B2B0B3";
	public static final int messagePeriod = 1; // number of seconds between two messages(ID28)
	
	public static SerialPort serialPort = new SerialPort("/dev/tty.usbserial");
	public static File file = new File("./GPS_output.out");

    public static Scanner keyboard = new Scanner(System.in);
	
	public static void main(String[] args) {
		ZonedDateTime utc = ZonedDateTime.now(ZoneOffset.UTC);
		try{
			setUpPort(serialPort);
			switchToSirf();
			ServerConnector.establishConnection();
			if (ServerConnector.isConnected == true) {addListenerAndVerifySwitch();} else {
				System.out.println("problem");
				serialPort.closePort();
			}
			sendCommand(pollClock);
//			RinexManipulator.createNewFile("./home" + utc.getYear() + utc.getMonthValue() + utc.getDayOfMonth() + ".rinex");
			stopReading();
		} catch (Exception ex) {
			ex.printStackTrace();
		}
	}
	
	public static void startAction() {
		try {
			sendCommand(setMessage28_1);
//			sendCommand(getClockMessage_2);
		} catch (SerialPortException e) {
		}
	}
	
	public static void disableAll() throws SerialPortException {
		sendCommand(disableAllMessages);
	}

	private static void switchToSirf() throws SerialPortException {
		serialPort.writeString("$PSRF100,0,4800,8,1,0*0F\r\n");
	}

	private static void sendCommand(String command) throws SerialPortException {
		serialPort.writeBytes(toByteArray(command));
	}

	private static void stopReading() throws SerialPortException {
		if (keyboard.nextLine().equals("stop")) {
			serialPort.closePort();
			keyboard.close();
			ServerConnector.closeAll();
		}
	}

	private static void addListenerAndVerifySwitch() throws SerialPortException {
		disableAll();
		setUpListener(serialPort);
		sendCommand(pollVersion);
	}

	private static void setUpListener(SerialPort serialPort) throws SerialPortException {
		serialPort.setEventsMask(SerialPort.MASK_RXCHAR);
		serialPort.addEventListener(new EventListener(serialPort));
	}

	private static void setUpPort(SerialPort serialPort) throws SerialPortException {
		serialPort.openPort();
		serialPort.setParams(4800, 8, 1, 0);
	}
	
	public static byte[] toByteArray(String s) {
	    return DatatypeConverter.parseHexBinary(s);
	}
	

}
