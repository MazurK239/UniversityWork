package com.home.diploma;

public class DateClass {

	public static int[] daysInMonths = {25, 0, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
	
	private static int year;
	private static int month;
	private static int day;
	private static int startOfTheWeek;
	private static int hour;
	private static int mins;
	private static double secs;
	private static double gpsTime = 0;
	private static String fullDate = "";
	private static boolean updateDay = false;
	
	
	public static void calculateRealDate(int gpsWeek) {
		System.out.println("started");
		int days = gpsWeek * 7;
		int years = (int)(days / 365.2425);
		year = 1980 + years;
		days = days - years * 365 - ((years - 1) / 4 + 1); // in brackets - number of leap years since the beginning of 1980 
		daysInMonths[1] = ((year % 4 == 0) && (year % 100 != 0)) || (year % 400 == 0) ? 29 : 28; // February
		for (int i = 0; i < 12; i++) {
			if (days > daysInMonths[i]) {
				days -= daysInMonths[i];
			} else {
				month = i + 1;
				startOfTheWeek = days;
				break;
			}
		}
		updateDay = true;
	}
	
	public static void calculateRealTime(double seconds) {
		if (updateDay) {
			day = startOfTheWeek + (int)seconds / 86400;
			if (day > daysInMonths[month-1]) {
				day = 1;
				month++;
				if (month > 12) {
					month = 1;
					year++;
				}
			}
			updateDay = false;
		}
		double dailyPart = seconds - (int)seconds / 86400 * 86400;
		hour = (int)dailyPart / 3600;
		mins = (int)(dailyPart - hour * 3600) / 60;
		secs = (double)(dailyPart - hour * 3600 - mins * 60);
		createDateString();		
	}
	
	private static void createDateString() {
		fullDate = "\n" + year + " " + month + " " + day + " " + hour + " " + mins + " " + String.format("%.8f", secs) + "\n";
	}
	
	public static String getDateString() {
		return fullDate;
	}
	
	public static void sendDateString() {
//		System.out.println("sending date string");
		ServerConnector.addLine(fullDate);
	}
	
	public static boolean isDifferentTime(double seconds) {
		boolean bool = (seconds != gpsTime) ? true : false;
		gpsTime = seconds;
		return bool;
	}

	public static int getYear() {
		return year;
	}

	public static int getMonth() {
		return month;
	}

	public static int getDay() {
		return day;
	}

	public static void updateDay() {
		updateDay = true;
	}

}
