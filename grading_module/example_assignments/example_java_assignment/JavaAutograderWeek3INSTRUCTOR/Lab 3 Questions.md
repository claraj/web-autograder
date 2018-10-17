# Lab 3

### Question 1 MPG

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
 
 
Make sure you use the name `mpg` for your method, since the test expects to find a method with that name.
The method takes two arguments, miles driven and gas used, in that order.

### Question 2 Do You Need A Hat?

You have a client who likes to wear a hat when the temperature is at or below 40F.
Write a method called doYouNeedAHat which takes one argument, the current temperature in Fahrenheit, as a double.

This method will return true if the temperature is at or below 40F.
This method will return false if the temperature is above 40F.

As before, make sure you use the name `doYouNeedAHat` for your method, and make sure you use the correct argument and return type.


### Question 3 Agile or Waterfall

Write a program that can help decide if a particular programming project
is best solved using a Waterfall or Agile methodology.

Your program should ask the user:

*	How many programmers will be on the team.  More than 30 programmers -> Waterfall
*	If there needs to be firm deadlines and a fixed schedule. Yes - > Waterfall
*	If the programmers have experience in requirements, analysis and testing as well as coding. Yes - > Agile
*	If there are stringent quality control requirements. Yes -> Waterfall 
*	If early integration is desirable.    Yes -> Agile
*	If the customer will be requiring working models early in the process. Yes -> Agile 

There's a `yesNoInput` method in the InputUtils library that returns boolean values from yes/no user input.
(If the user types 'n' or 'no', the method returns false. If the user types 'y' or 'yes' the method returns true.)

Write a method called agileOrWaterfall, which takes this data as integer and boolean arguments.
**The arguments should be provided in the order given above**.
`agileOrWaterfall` will return a String, a suggestion on whether Agile, or Waterfall, or either, may be best.

To decide, check how many factors are in favor of Agile. If there are 4 or more factors in favor of Agile, then return `AGILE`.
If there are 4 or more factors in favor of Waterfall, return `WATERFALL`.
If there are an equal number of factors in favor of Agile and Waterfall, returns `EITHER`.

Notice that there are three global constants `AGILE`, `WATERFALL` and `EITHER`. Your `agileOrWaterfall` method should return one of these Strings. 

Use your `agileOrWaterfall` method in your program to suggest which methodology to use.

Your main method should do all of the asking questions and printing the result.
Your agileOrWaterfall method should be given the relevant data, and do the processing,
deciding, and returning the result.


### Question 4 Reduce Repetition

Start with the `Question_4_Reduce_Repetition.java` program.
 
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
 
 
### Question 5 Count Uppercase Letters

Write a method called countUppercase that takes a String array argument.
You can assume that every element in the array is a one-letter String, for example

`String[] test = { "a", "B", "c", "D", "e"};`

This method will count the number of uppercase letters from the set A through Z in the array, 
and return that number.  So for the example array above, your method will return 2. 

You will need to use some Java library methods. You may need some methods from
some or all of these library classes: String, Character, Integer.
  
### Question 6 Marathon
      
You have a friend who wants to run a marathon race, which is 26.2 miles.
Currently, your friend can run exactly 1 mile.  Your friend's plan is to
try to run 10% further every week, until they can run the entire
marathon distance.

So in the first week of training, they will run 1 mile;  
in the second week 1.1 miles,  
int the third week 1.21 miles...  

You would like to write a program to print out their training schedule.

But, what if your friend thinks this schedule is too slow? Or too fast?
Your friend can get to the marathon distance sooner by increasing their distance
by 15% every week?  Or, they may want to be more leisurely and increase by 3% every week.
How does that affect the number of weeks needed?

Then, you think, what if your friend decides they want to train for a
10 mile race? Or a 100 mile race?

What if you friend starts with the ability to run 5 miles?

Write a method that takes 3 arguments:
 - the current distance your friend can run,
 - the target distance
 - the percent increase. This should be expressed as 5 for 5%, 10 for 10%.

In your method, use a loop to calculate the distance they need to run every
week until they can run the target distance.

The method should print the weekly distance data as a table.
Use string formatting to display the weekly distances to 2 decimal places.

The method should return the number of weeks it will take, as an integer.
