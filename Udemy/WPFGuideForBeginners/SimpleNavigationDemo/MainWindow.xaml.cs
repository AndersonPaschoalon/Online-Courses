using SimpleNavigationDemo.Pages;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace SimpleNavigationDemo
{
    /// <summary>
    /// Interação lógica para MainWindow.xam
    /// </summary>
    public partial class MainWindow : Window
    {
        public Page1 page1;
        public Page2 page2;
        public Page3 page3;



        public MainWindow()
        {
            InitializeComponent();
            page1 = new Page1();
            page2 = new Page2();
            page3 = new Page3();

            page3.GoToPage1ButtonClick += Button_Click_1;
            page2.GoToPage1ButtonClick += Button_Click_1;
            page2.GoToPage3ButtonClick += Button_Click_3;

        }
        private void Button_Click_1(object sender, RoutedEventArgs e) 
        {
            MainWindowFrame.Content = page1;

        }

        private void Button_Click_2(object sender, RoutedEventArgs e)
        {
            MainWindowFrame.Content = page2;
        }

        private void Button_Click_3(object sender, RoutedEventArgs e)
        {
            MainWindowFrame.Content = page3;
        }

        private void Back_Button_Click(object sender, RoutedEventArgs e)
        {
            if (MainWindowFrame.NavigationService.CanGoBack)
            {
                MainWindowFrame.NavigationService.GoBack();
            }
            else 
            {
                Console.WriteLine("cant go back");
            }
        }

        private void Forw_Button_Click(object sender, RoutedEventArgs e)
        {
            if (MainWindowFrame.NavigationService.CanGoForward)
            {
                MainWindowFrame.NavigationService.GoForward();
            }
            else
            {
                Console.WriteLine("cant go forw");
            }

        }
    }
}
