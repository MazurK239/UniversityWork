package com.home.diploma;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;

public class ServerConnector {
	
	static String CRLF = "\r\n";
	static PrintWriter writer;
	static BufferedReader in;
	static Socket connection;
	static boolean isConnected = false;
	
	public static void establishConnection() throws IOException {
		
		InetAddress caster = InetAddress.getByName("gnss.pu.ru");
		connection = new Socket(caster, 6669);
		writer = new PrintWriter(connection.getOutputStream(), true);
		in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
		
		if (caster.isReachable(35000)) {
			writer.println("SOURCE sesam01 /HOME" + CRLF + "Source-Agent: NTRIP" + CRLF);
		} else {
			System.out.println("not reachable");
		}
		String response = in.readLine();
		if (response.contains("OK")) {
			isConnected = true;
			System.out.println("Connection established");
		} else {
			System.out.println(response);
		}
	}

	public static void addLine(String line) {
		try {
			writer.println(line + CRLF);
		} catch (Exception ex) {
			
		}
	}
	
	public static void closeAll() {
		writer.close();
		try {
			in.close();
			connection.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}
