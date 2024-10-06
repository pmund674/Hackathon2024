package application;

import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

import java.util.*;

class Event {
    int startHour;
    int endHour;
    String name;

    public Event(int startHour, int endHour, String name) {
        this.startHour = startHour;
        this.endHour = endHour;
        this.name = name;
    }
}

class ScheduleBuilder {
    Map<String, List<Event>> schedule;

    public ScheduleBuilder() {
        schedule = new HashMap<>();
    }

    public void blockTime(int year, int month, int day, int startHour, int endHour, String name) {
        String date = year + "/" + month + "/" + day;
        schedule.putIfAbsent(date, new ArrayList<>());
        schedule.get(date).add(new Event(startHour, endHour, name));
    }

    public String viewSchedule(int year, int month, int day) {
        StringBuilder result = new StringBuilder();
        String date = year + "/" + month + "/" + day;
        if (schedule.containsKey(date)) {
            result.append("Schedule for ").append(month).append("/").append(day).append("/").append(year).append(":\n");
            for (Event event : schedule.get(date)) {
                result.append(event.startHour).append(":00 - ").append(event.endHour).append(":00: ").append(event.name).append("\n");
            }
        } else {
            result.append("No schedule for ").append(month).append("/").append(day).append("/").append(year);
        }
        return result.toString();
    }

    public void deleteEvent(int year, int month, int day, int startHour, String name) {
        String date = year + "/" + month + "/" + day;
        if (schedule.containsKey(date)) {
            Iterator<Event> iterator = schedule.get(date).iterator();
            while (iterator.hasNext()) {
                Event event = iterator.next();
                if (event.startHour == startHour && event.name.equals(name)) {
                    iterator.remove();
                    return;
                }
            }
        }
    }

    public void addRecurringEvent(int year, int month, int day, int startHour, int endHour, String name, int frequency) {
        for (int i = 0; i < frequency; i++) {
            blockTime(year, month, day + i, startHour, endHour, name);
        }
    }
}

public class Main extends Application {
    ScheduleBuilder builder = new ScheduleBuilder();

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) {
        primaryStage.setTitle("Schedule Manager");

        // Creating input fields
        TextField yearField = new TextField();
        TextField monthField = new TextField();
        TextField dayField = new TextField();
        TextField startHourField = new TextField();
        TextField endHourField = new TextField();
        TextField nameField = new TextField();
        TextField frequencyField = new TextField();
        
        TextArea outputArea = new TextArea();
        outputArea.setEditable(false);
        
        // Creating buttons
        Button blockTimeButton = new Button("Block Time");
        Button viewScheduleButton = new Button("View Schedule");
        Button deleteEventButton = new Button("Delete Event");
        Button addRecurringButton = new Button("Add Recurring Event");
        
        // Setting up button actions
        blockTimeButton.setOnAction(e -> {
            int year = Integer.parseInt(yearField.getText());
            int month = Integer.parseInt(monthField.getText());
            int day = Integer.parseInt(dayField.getText());
            int startHour = Integer.parseInt(startHourField.getText());
            int endHour = Integer.parseInt(endHourField.getText());
            String name = nameField.getText();
            builder.blockTime(year, month, day, startHour, endHour, name);
            outputArea.appendText("Time blocked successfully!\n");
        });

        viewScheduleButton.setOnAction(e -> {
            int year = Integer.parseInt(yearField.getText());
            int month = Integer.parseInt(monthField.getText());
            int day = Integer.parseInt(dayField.getText());
            String schedule = builder.viewSchedule(year, month, day);
            outputArea.setText(schedule);
        });

        deleteEventButton.setOnAction(e -> {
            int year = Integer.parseInt(yearField.getText());
            int month = Integer.parseInt(monthField.getText());
            int day = Integer.parseInt(dayField.getText());
            int startHour = Integer.parseInt(startHourField.getText());
            String name = nameField.getText();
            builder.deleteEvent(year, month, day, startHour, name);
            outputArea.appendText("Event deleted successfully!\n");
        });

        addRecurringButton.setOnAction(e -> {
            int year = Integer.parseInt(yearField.getText());
            int month = Integer.parseInt(monthField.getText());
            int day = Integer.parseInt(dayField.getText());
            int startHour = Integer.parseInt(startHourField.getText());
            int endHour = Integer.parseInt(endHourField.getText());
            String name = nameField.getText();
            int frequency = Integer.parseInt(frequencyField.getText());
            builder.addRecurringEvent(year, month, day, startHour, endHour, name, frequency);
            outputArea.appendText("Recurring event added successfully!\n");
        });

        // Layout
        GridPane grid = new GridPane();
        grid.setPadding(new Insets(10));
        grid.setVgap(10);
        grid.setHgap(10);
        
        grid.add(new Label("Year:"), 0, 0);
        grid.add(yearField, 1, 0);
        grid.add(new Label("Month:"), 0, 1);
        grid.add(monthField, 1, 1);
        grid.add(new Label("Day:"), 0, 2);
        grid.add(dayField, 1, 2);
        grid.add(new Label("Start Hour:"), 0, 3);
        grid.add(startHourField, 1, 3);
        grid.add(new Label("End Hour:"), 0, 4);
        grid.add(endHourField, 1, 4);
        grid.add(new Label("Event Name:"), 0, 5);
        grid.add(nameField, 1, 5);
        grid.add(new Label("Frequency (recurring):"), 0, 6);
        grid.add(frequencyField, 1, 6);

        grid.add(blockTimeButton, 0, 7);
        grid.add(viewScheduleButton, 1, 7);
        grid.add(deleteEventButton, 0, 8);
        grid.add(addRecurringButton, 1, 8);
        grid.add(outputArea, 0, 9, 2, 1);

        Scene scene = new Scene(grid, 400, 500);
        primaryStage.setScene(scene);
        primaryStage.show();
    }
}
