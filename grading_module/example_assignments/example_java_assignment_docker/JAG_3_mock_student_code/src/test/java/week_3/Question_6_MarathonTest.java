package week_3;

import java.lang.reflect.Method;
import java.util.regex.Pattern;

import static junit.framework.TestCase.assertEquals;
import static junit.framework.TestCase.assertTrue;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.fail;
import static test_utils.MethodUtil.findMethod;
import static test_utils.PrintUtils.*;


import org.junit.Before;
import org.junit.Test;


public class Question_6_MarathonTest {
    
    private Method training;
    private Question_6_Marathon q2;
    
    @Before
    public void findTrainingMethod(){
        
        // Find trainingSchedule method that student has created
        training = findMethod("week_3.Question_6_Marathon", "trainingSchedule", new Class[]{double.class, double.class, double.class});
        q2 = new Question_6_Marathon();
        
    }
    
    @Test(timeout=3000)
    public void testTrainingScheduleWeeks() {
        
        try {
            
            int weeks = (int) training.invoke(q2, 3, 5, 20);
            assertEquals("When called with a starting distance of 3 miles and target of 5 miles, and 20% distance increase, the number of weeks should be 4", 4, weeks);
            
            // And some more test data, check the number of weeks is correct
            
            weeks = (int) training.invoke(q2, 1, 20, 5);
            assertEquals("When called with a starting distance of 1 mile and target of 20 miles, and 5% distance increase, the number of weeks should be 63", 63, weeks);
            
            weeks = (int) training.invoke(q2, 1, 26.2, 5);
            assertEquals("Start 1 mile, target 26.2, increase 5% should be 68 weeks", 68, weeks);
            
            weeks = (int) training.invoke(q2, 10, 100, 8);
            assertEquals("Start 10 miles, target 100, increase 8% should be 31 weeks", 31, weeks);
            
        } catch (Exception e) {
            fail("Check your trainingSchedule method has the right name, right parameters, right return type, " +
                    "\nand does not throw any exceptions when it runs. Check the instructions for the types required. " +
                    "\nError message:" + e.toString());
        }
        
    }
    
    
    @Test(timeout=3000)
    public void testTrainingScheduleTable() throws Exception {
        
        catchStandardOut();   // Save everything the program prints to the terminal.
        
        training.invoke(q2, 3, 5, 20);   // don't care what is returned, tested it in method above.
        
        String printedOutput = resetStandardOut();  // Restore regular printing behavior
        
        // Check the output from the first call to the training method (start 3 miles, target 5, increase 20%. 4 weeks total.
        printedOutput = printedOutput.replace("\n", " ");
        printedOutput = printedOutput.replace("\r", " ");
        
        // Week 1 3.00, Week 2 3.60, Week 3 4.32, Week 4 5.18, to 2 decimal places.
        String expectedPatternRegex = ".*1.*3.0.*2.*3.60.*3.*4.32.*4.*5.18.*";
        
        assertTrue("Check that your table is printing every row of the training schedule. If you think your code is correct, please alert Clara", Pattern.matches(expectedPatternRegex, printedOutput));
        
        // Check that there are no numbers with more than 2 decimal places
        
        String moreThan2decimalPlaces = ".*\\d*\\.[\\d]{3,}.*";
        assertFalse("Display numbers with 2 decimal places. Use String.format() OR System.out.printf(). \nExample:  \n\tString.format(\"Distance %.2f miles\", 1.2345) \nwill generate the string \"Distance 1.23 miles\" " , Pattern.matches(moreThan2decimalPlaces, printedOutput));
        
    }
    
    
}
    
