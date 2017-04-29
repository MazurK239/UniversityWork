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

public class SirfRead {

	private static SerialPort serialPort;
	private static File file = new File("./GPS_output.out");
	private static OutputStream fos;

    public static void main() {
    	try {
			fos = new FileOutputStream(file);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
        serialPort = new SerialPort("/dev/tty.usbserial");
        Scanner keyboard = new Scanner(System.in);
        try {
            serialPort.openPort();
            System.out.println("opened port");
            serialPort.setParams(SerialPort.BAUDRATE_4800, SerialPort.DATABITS_8, SerialPort.STOPBITS_1, SerialPort.PARITY_NONE);
            System.out.println("set params");
            serialPort.setEventsMask(SerialPort.MASK_RXCHAR);
            System.out.println("started reading");
            serialPort.addEventListener(new EventListener());
            if (keyboard.nextLine().equals("stop")) {
            	serialPort.closePort();
            	System.out.println("stopped reading");
            }
        }
        catch (SerialPortException ex) {
            System.out.println(ex);
        }
    }

    private static class EventListener implements SerialPortEventListener {

        public void serialEvent(SerialPortEvent event) {
            if(event.isRXCHAR() && event.getEventValue() > 0){
                try {
                    byte[] buffer = serialPort.readBytes(event.getEventValue());
                    fos.write(buffer, 0, buffer.length);
                } catch (Exception e) {
					e.printStackTrace();
				}
            }
        }
    }
}
