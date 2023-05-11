import java.util.*;
public class q1 {


    public static void main (String [] args){
        Scanner sc= new Scanner(System.in);
        System.out.println("this is...");
        while (true)
        {
            System.out.println("please enter 1 for a rectangle tower, 2 for a triangle tower" +
                    "and 3 to exit");
            //i get the user decision
            int option = sc.nextInt();
            //exit decision
            if (option == 3)
                return;
            //not a legal decision
            if (option != 1 && option != 2)
                System.out.println("not a legal option");
            else{
                System.out.println("please enter your tower height");
                int height = sc.nextInt();
                System.out.println("please enter your tower width");
                int width = sc.nextInt();
                if (option == 1)
                    rectangleOption(height, width);
                else
                    triangleOption(height, width);
            }
        }
    }

    private static void rectangleOption(int height, int width) {
        //print the area
        if (height == width || Math.abs(height-width) > 5)
            System.out.println("your tower area is " + height*width);
        //print the scope
        else
            System.out.println("your tower scope is " + (height*2)+(width*2));
    }

    private static void triangleOption(int height, int width) {
        Scanner scan = new Scanner(System.in);
        System.out.println("to calculate the tower scope choose 1, to print the tower choose 2");
        int option = scan.nextInt();
        //print the tower scope
        if (option == 1){
            double result = Math.sqrt(Math.pow(height, 2)+Math.pow(width, 2)) + width;
            System.out.println("your tower scope is:" + result);
        }
        //send to a private method to print the tower
        else if (option == 2)
            printTower(height, width);
        else
            System.out.println("not a legal option");
    }

    private static void printTower(int height, int width) {
        //make sure this tower can be printed
        if (width % 2 == 0 || width > (2*height)) {
            System.out.println("sorry' this tower cannot be printed");
            return;
        }
        //this is the number of lines to each odd number between 1 and the width
        int lenNum = (height-2)/(((width-4)/2)+1);
        //the rest lines will be printed with 3 *
        int mod = (height-2)%(((width-4)/2)+1);
        //for each odd number between 1 and the width
        for (int i = 1; i <= width; i+=2)
        {
            if (i == 1 || i == width)//in this case we print only one line.
            {
                System.out.println("");
                //move to the right place in the line:
                for (int j = 0; j < (width-i)/2; j++)
                    System.out.print(" ");
                //print the line:
                for (int j = 0; j < i; j++)
                    System.out.print("*");
            }
            else
            {
                for (int k = 0; k < lenNum; k++)
                {
                    System.out.println("");
                    //move to the right place in the line:
                    for (int j = 0; j < (width-i)/2; j++)
                        System.out.print(" ");
                    //print the line:
                    for (int j = 0; j < i; j++)
                        System.out.print("*");
                }
                if (i == 3){
                    //print the extra lines for the top group
                    for (int k = 0; k < mod; k++)
                    {
                        System.out.println("");
                        //move to the right place in the line:
                        for (int j = 0; j < (width-i)/2; j++)
                            System.out.print(" ");
                        //print the line:
                        for (int j = 0; j < i; j++)
                            System.out.print("*");
                    }
                }
            }
        }
        System.out.println("");
    }


}
