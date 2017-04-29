package com.home.diploma;

import jssc.SerialPort;
import jssc.SerialPortEvent;
import jssc.SerialPortEventListener;

public class EventListener implements SerialPortEventListener {
	public SerialPort serialPort;

	public EventListener(SerialPort port) {
		serialPort = port;
	}
	
	public void serialEvent(SerialPortEvent event) {
        if(event.isRXCHAR() && event.getEventValue() > 0){
            try {
                byte[] buffer = serialPort.readBytes(event.getEventValue());
                MessageParser2.processByte(buffer);
            } catch (Exception e) {
				e.printStackTrace();
			}
        }
    }
}