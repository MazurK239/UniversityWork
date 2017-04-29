package com.home.diploma;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.OutputStream;
import java.util.Scanner;

import jssc.SerialPort;
import jssc.SerialPortEvent;
import jssc.SerialPortEventListener;
import jssc.SerialPortException;

import javax.xml.bind.DatatypeConverter;

public class SendSirfCommand {
	
	private static String pollClock = "A0A2000290000090B0B3";
	private static String pollVersion = "A0A2000284000084B0B3"; 
	private static String disableAllMessages = "A0A20008A60202000000000000AAB0B3"; 
	private static String getMessage28_1 = "A0A20008A6001C010000000000C3B0B3"; // period = 1 second
	private static String getMessage28_5 = "A0A20008A6001C050000000000C7B0B3"; // period = 1 second
	private static String getMessage28_10 = "A0A20008A6001C0A0000000000CCB0B3"; // period = 10 seconds
	private static String getClockMessage_1 = "A0A20008A60007010000000000AEB0B3";
	private static String getClockMessage_5 = "A0A20008A60007050000000000B2B0B3";

    private static SerialPort serialPort;
    private static File file = new File("./GPS_output.out");
    private static OutputStream fos;
	
	public static void main(String[] args) {
		try {
			fos = new FileOutputStream(file);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		serialPort = new SerialPort("/dev/tty.usbserial");
        Scanner keyboard = new Scanner(System.in);
		try {
			serialPort.openPort();
			serialPort.setParams(4800, 8, 1, 0);
			serialPort.writeBytes(toByteArray(disableAllMessages));
			serialPort.setEventsMask(SerialPort.MASK_RXCHAR);
            System.out.println("started reading");
            serialPort.addEventListener(new EventListener());
            
            serialPort.writeBytes(toByteArray(pollVersion));
            serialPort.writeBytes(toByteArray(getMessage28_1));
            serialPort.writeBytes(toByteArray(getClockMessage_1));
            
            if (keyboard.nextLine().equals("stop")) {
            	serialPort.closePort();
            	keyboard.close();
            	System.out.println("stopped reading");
            }
		} catch (SerialPortException e) {
			e.printStackTrace();
		}
	}
	
	public static byte[] toByteArray(String s) {
	    return DatatypeConverter.parseHexBinary(s);
	}
	
	private static class EventListener implements SerialPortEventListener {

        public void serialEvent(SerialPortEvent event) {
            if(event.isRXCHAR() && event.getEventValue() > 0){
                try {
                    byte[] buffer = serialPort.readBytes(event.getEventValue());
//                    fos.write(buffer, 0, buffer.length);
                    MessageParser.processByte(buffer);
                    
                } catch (Exception e) {
					e.printStackTrace();
				}
            }
        }

    }
	
}
