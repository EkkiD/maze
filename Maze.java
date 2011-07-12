//
//  Maze.java
//  
//
//  Created by Erick Dransch on 10-05-23.
//  Copyright 2010 University of Waterloo. All rights reserved.
//

import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.geom.Line2D;
import java.awt.Color;
//import basic swing
import javax.swing.*;    

public class Maze extends JPanel{
	
	static int maze[][] = new int[15][15];
	
	public static void printMaze(Graphics2D aGraphics)
	{
                
                Line2D line = new Line2D.Float(25, 25, 425, 25);
                aGraphics.draw(line);
                line = new Line2D.Float(25, 25, 25, 425);
                aGraphics.draw(line);
                line = new Line2D.Float(425, 25, 425, 425);
                aGraphics.draw(line);
                line = new Line2D.Float(25, 425, 425, 425);
                aGraphics.draw(line);
                aGraphics.setPaint(Color.blue);
		for (int i=25; i<425; i+=25)
		{
			for (int j=25; j<425; j +=25)
			{       
                                if (i != 25)
                                {
                                        Line2D lin = new Line2D.Float(i, j+2, i, j+23);
                                        aGraphics.draw(lin);
                                }
                                if (j != 25)
                                {
                                        Line2D lin2 = new Line2D.Float(i+2, j, i+23, j);
                                        aGraphics.draw(lin2);
                                }
			}
			
		}
	}
        
        
        /**
         * This is the method where the line is drawn.
         *
         * @param g The graphics object
         */
        public void paint(Graphics g) {
                Graphics2D g2 = (Graphics2D) g;
                printMaze(g2);
        }
        /**
         * Create the GUI and show it.  For thread safety,
         * this method should be invoked from the
         * event-dispatching thread.
         */
        
        private static void createAndShowGUI() {
                Maze maze1 = new Maze();
                //Create and set up the window.
                JFrame frame = new JFrame("Erick's Maze Generator");
                frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                
                //Add the ubiquitous "Hello World" label.
                JLabel label = new JLabel("Hello World");
                
                frame.add(maze1);
                //frame.getContentPane().add(label);
                
                //Display the window.
                frame.setSize(450,450);
                frame.setVisible(true);
                
        }
        
	public static void main(String[] args) 
	{
                //Schedule a job for the event-dispatching thread:
                //creating and showing this application's GUI.
                javax.swing.SwingUtilities.invokeLater(new Runnable() {
                        public void run() {
                                createAndShowGUI();
                        }
                });
	}//end of main
        
}//end maze class
