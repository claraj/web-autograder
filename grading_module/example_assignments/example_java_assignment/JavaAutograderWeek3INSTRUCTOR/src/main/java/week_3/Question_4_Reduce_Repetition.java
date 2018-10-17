package week_3;

import static input.InputUtils.*;

/**

 Refactor this program to make it less repetitive.
 
 Notice there are several drinks, and the code to get the total sales for each is very similar.
 Can you create a new method that will be called from the coffeeShop method,
 to make this program less repetitive?

 Hint: create a method that takes the name of a drink as an argument.
 This method can ask the user for data about that drink, calculate sales for that drink, and return the sales for that drink.

 Hint: You are going to call your new method 5 times. But don't write 5 lines of code to call the method! 5 times is manageable, but what if there were 100 drinks?
 Can you use an array of drink names, and a loop? Your drinks are

 String[] drinks = { "coffee", "hot chocolate", "tea", "cappuccino", "mocha"};

 The total lines of code in your program should get smaller. BUT, don't just delete lines,
 or compress more than one line together. Your code will be reviewed for clarity, readability, and logic.

 */


public class Question_4_Reduce_Repetition {


    // Don't modify this line
    public static void main(String[] args) {
        new Question_4_Reduce_Repetition().coffeeShop();
    }


    public void coffeeShop() {

        System.out.println("Coffee Shop Sales Calculator Program");

        double totalSales = 0;

        int coffeeCups = intInput("How many cups of coffee did you sell today?");
        double coffeePrice = doubleInput("What does a cup of coffee cost?");
        double coffeeDrinkSales = coffeeCups * coffeePrice;
        totalSales = totalSales + coffeeDrinkSales;

        int chocolateCups = intInput("How many cups of hot chocolate did you sell today?");
        double chocolatePrice = doubleInput("What does a cup of hot chocolate cost?");
        double chocolateDrinkSales = chocolateCups * chocolatePrice;
        totalSales = totalSales + chocolateDrinkSales;

        int teaCups = intInput("How many cups of tea did you sell today?");
        double teaPrice = doubleInput("What does a cup of tea cost?");
        double teaDrinkSales = teaCups * teaPrice;
        totalSales = totalSales + teaDrinkSales;

        int cappuccinoCups = intInput("How many cups of cappuccino did you sell today?");
        double cappuccinoPrice = doubleInput("What does a cup of cappuccino cost?");
        double cappuccinoDrinkSales = cappuccinoCups * cappuccinoPrice;
        totalSales = totalSales + cappuccinoDrinkSales;

        int mochaCups = intInput("How many cups of mocha did you sell today?");
        double mochaPrice = doubleInput("What does a cup of mocha cost?");
        double mochaDrinkSales = mochaCups * mochaPrice;
        totalSales = totalSales + mochaDrinkSales;
        
        System.out.println("Total sales for the day are $"  + totalSales);

    }

}

