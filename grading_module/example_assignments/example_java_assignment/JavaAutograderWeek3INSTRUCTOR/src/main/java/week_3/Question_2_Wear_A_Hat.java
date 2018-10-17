package week_3;

/**

 You have a client who likes to wear a hat when the temperature is at or below 40F.
 Write a method called doYouNeedAHat which takes one argument, the current temperature in Fahrenheit, as a double.

 This method will return true if the temperature is at or below 40F.
 This method will return false if the temperature is above 40F.

 */

import static input.InputUtils.doubleInput;

public class Question_2_Wear_A_Hat {

    // You don't need to modify this.
    public static void main(String[] args) { new Question_2_Wear_A_Hat().doYouNeedAHatToday(); }


    public void doYouNeedAHatToday() {

        double todayTemperature = doubleInput("Enter today's temperature, in fahrenheit.");

        // TODO Call your new doYouNeedAHat method with todayTemperature as the argument.
        // TODO Use the return value from doYouNeedAHat to print a message to the user, telling them if they need a hat or not.

    }


    // TODO create the new public doYouNeedAHat method here.
    // doYouNeedAHat should have one argument, a double, representing the temperature.
    // doYouNeedAHat should return a boolean.
    // If the temperature is at or below 40F, return true.
    // If the temperature is above 40F, return false.


}
