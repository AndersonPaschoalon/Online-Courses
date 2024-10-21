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

namespace LinqDemo
{
    /// <summary>
    /// Interação lógica para MainWindow.xam
    /// </summary>
    public partial class MainWindow : Window
    {

        List<int> myList;

        public MainWindow()
        {
            InitializeComponent();
            myList = new List<int>() { 4, 5, 6, 7, 8, 9, 0, 1, 2, 3};
            MyTextBlock.Text = StrigifyList(myList);
        }

        public string StrigifyList(List<int> inList) 
        {
            string csv = "";
            foreach (int item in inList) 
            {    
                csv += item.ToString() + ",";
            }
            csv.TrimEnd(',');
            return csv;
        }

        public List<int> FilterListOddNumbers(List<int> inList) 
        {
            return inList.Where(i => (i%2) != 0).ToList();
        }

        public List<int> FilterListEvenNumbers(List<int> inList)
        {
            return inList.Where(i => (i % 2) == 0).ToList();
        }

        public List<int> SortAscending(List<int> inList) 
        {
            return inList.OrderBy(i => i).ToList();
        }

        public List<int> SortDescend(List<int> inList)
        {
            return inList.OrderByDescending(i => i).ToList();
        }


        private void Odd_Click(object sender, RoutedEventArgs e)
        {
            MyTextBlock.Text = StrigifyList(FilterListOddNumbers(myList));
        }

        private void Even_Click(object sender, RoutedEventArgs e)
        {
            MyTextBlock.Text = StrigifyList(FilterListEvenNumbers(myList));
        }

        private void RemoveFilter_Click(object sender, RoutedEventArgs e)
        {
            MyTextBlock.Text = StrigifyList(myList);
        }

        private void Ascending_Click(object sender, RoutedEventArgs e)
        {
            MyTextBlock.Text = StrigifyList(SortAscending(myList));
        }

        private void Descending_Click(object sender, RoutedEventArgs e)
        {
            MyTextBlock.Text = StrigifyList(SortDescend(myList));
        }
    }
}
