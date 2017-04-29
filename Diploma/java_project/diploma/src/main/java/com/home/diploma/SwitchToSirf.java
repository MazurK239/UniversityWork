package com.home.diploma;

import jssc.SerialPort;
import jssc.SerialPortException;

public class SwitchToSirf {

	private static SerialPort serialPort;
	
	public static void main(String[] args) {
		serialPort = new SerialPort("/dev/tty.usbserial");
		try {
			serialPort.openPort();
			serialPort.setParams(4800, 8, 1, 0);
			serialPort.writeString("$PSRF100,0,4800,8,1,0*0F\r\n");
			serialPort.closePort();
			System.out.println("successful!");
		} catch (SerialPortException e) {
			e.printStackTrace();
		}
	}
	
}
