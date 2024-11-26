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
using WindowsStoreClone.Pages;
using WindowsStoreClone.UserControls;

namespace WindowsStoreClone
{
    /// <summary>
    /// Interação lógica para MainWindow.xam
    /// </summary>
    public partial class MainWindow : Window
    {
        private MainPage MainWindowContentPage;
        public MainWindow()
        {
            InitializeComponent();
            MainWindowContentPage = new MainPage();
            MainWindowContentPage.AppClicked += MainWindowContentPage_AppClicked;
        }

        private void MainWindowContentPage_AppClicked(AnApp sender, RoutedEventArgs e)
        {
            AnApp senderApp = (AnApp)sender;
            Console.WriteLine("MainWindow received Click Event!");
            Console.WriteLine($"---- senderApp (sender):{senderApp.Name}");
            Console.WriteLine($"---- this.Name:{Name}");

            AppDetails myAppDetails = new AppDetails(sender);
            Console.WriteLine("MyAppDetails_BackButtonClicked");
            myAppDetails.BackButtonClicked += MyAppDetails_BackButtonClicked;
           
            MainWindowFrame.Content = myAppDetails;
        }

        private void MyAppDetails_BackButtonClicked(object sender, RoutedEventArgs e)
        {
            if (MainWindowFrame.NavigationService.CanGoBack)
            {
                Console.WriteLine("GoBack");
                MainWindowFrame.NavigationService.GoBack();
            }
        }

        private void MainWindowFrame_Loaded(object sender, RoutedEventArgs e)
        {
            //AppDetails myAppDetails = new AppDetails();
            MainWindowFrame.Content = MainWindowContentPage;
            //MainWindowFrame.Content = myAppDetails;
        }


    }
}
