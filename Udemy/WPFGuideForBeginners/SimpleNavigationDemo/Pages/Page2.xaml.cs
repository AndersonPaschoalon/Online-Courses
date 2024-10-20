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

namespace SimpleNavigationDemo.Pages
{
    /// <summary>
    /// Interação lógica para Page2.xam
    /// </summary>
    public partial class Page2 : Page
    {

        public delegate void OnGoToPage1ButtonClick(object sender, RoutedEventArgs e);
        public event OnGoToPage1ButtonClick GoToPage1ButtonClick;


        public delegate void OnGoToPage3ButtonClick(object sender, RoutedEventArgs e);
        public event OnGoToPage3ButtonClick GoToPage3ButtonClick;

        public Page2()
        {
            InitializeComponent();
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {

        }

        private void Button_Click_GoToPage1(object sender, RoutedEventArgs e)
        {
            GoToPage1ButtonClick(sender, e);
        }

        private void Button_Click_GoToPage3(object sender, RoutedEventArgs e)
        {
            GoToPage3ButtonClick(sender, e);
        }
    }
}
