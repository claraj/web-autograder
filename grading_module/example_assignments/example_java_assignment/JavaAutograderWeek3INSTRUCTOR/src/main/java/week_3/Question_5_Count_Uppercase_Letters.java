package week_3;

/**

 Write a method called countUppercase that takes a String array argument.
 You can assume that every element in the array is a one-letter String, for example
 String[] test = { "a", "B", "c", "D", "e"};

 This method will count the number of uppercase letters from the set A through Z in the array,
 and return that number.  So for the example array above, your method will return 2.

 You will need to use some Java library methods. You may need some methods from
 some or all of these library classes: String, Character, Integer.
 
 COMMENT YOUR CODE. As well as the tests, the instructor will also read your comments
 to verify that you understand and can describe the code you've written.
 
 */



public class Question_5_Count_Uppercase_Letters {

    public static void main(String[] args) {
        new Question_5_Count_Uppercase_Letters().countUppercaseLetters();
    }

    private void countUppercaseLetters() {

        // You can call your new countUppercase() method with these example arrays.

        String[] test1 = { "a", "b", "c" };  // no uppercase letters - your method should return 0
        String[] test2 = { "a", "B", "c", "D", "e" };  // two uppercase letters - your method should return 2
        String[] test3 = { "A", "B", "C", "D" };  // four uppercase letters - your method should return 4
        String[] test4 = { "$", "B", "c", "6", "D", "\n", "E" };  // three uppercase letters - your method should return 3

        // You don't need any user input in this program.
    }


    /*

    TODO Create a public method called countUppercase.

    This method should take a String array argument, and return an int.

    This method should count the number of uppercase letters - in the range A through Z - and return that count.

    */



}
