package week_3;

/**

 Write a program to calculate the MPG for a car journey.
 (MPG = Miles per gallon, calculate by dividing number of miles, by number of gallons of gas used).

 Write a method called mpg that has two arguments, in the following order:
 - a double to represent the number of miles driven, and
 - a double to represent the number of gallons of gas used on a car journey
 And returns a double value, representing the MPG for the journey.

 Your method should calculate and return the MPG for the car journey.  Your main method should
 -	Ask the user for the miles and gas used
 -	Call your method
 -	Use the returned value to display the MPG

 */

public class Question_1_MPG {

    // You don't need to modify this method.
    public static void main(String[] args) {
        new Question_1_MPG().mpgCalculations();
    }


    public void mpgCalculations() {

        // TODO Ask user for number of miles, as a double

        // TODO Ask user for gallons of gas used, as a double

        // TODO Call your new mpg method (that you'll write below) and save the returned miles-per-gallon value

        // TODO Print the return miles-per-gallon value.

    }


    // TODO After this method, create a method called mpg. This method will calculate and return the miles-per-gallon for a trip,
    // based on the miles driven and the gallons of gas used.
    // Your method should be public.
    // A public method declaration begins with the word public, for example in the calculate() method above.
    // The method needs to be public so the test can find it.

    // Make sure you use the name mpg since the test expects to find a method with that exact name.

    // The mpg method takes two parameters, miles driven and gas used, both doubles, *in that order*.

    // The mpg method should calculate and return the MPG for this journey.

    // The mpg method should use the two parameters (miles driven, and gas used) to calculate the miles-per-gallon.
    // The mpg method should not ask for any user input - get the user input in the calculate

}
