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

namespace WindowsStoreClone.UserControls
{
    /// <summary>
    /// Interação lógica para AppsViewer.xam
    /// </summary>
    public partial class AppsViewer : UserControl
    {

        List<AnApp> PresentedApps;

        public AppsViewer()
        {
            InitializeComponent();
            PresentedApps = new List<AnApp>();
            AppsList.ItemsSource = PresentedApps;
            for (int i = 0; i < 9; i++)
            {
                AnApp curr = new AnApp();
                PresentedApps.Add(curr);
            }
        }

        private void ScrollLeftButton_Click(object sender, RoutedEventArgs e)
        {
            int widthOfOneApp = (int)PresentedApps.First().ActualWidth + 2 * (int)PresentedApps.First().Margin.Left;
            AppsScrollView.ScrollToHorizontalOffset(AppsScrollView.HorizontalOffset - 1*widthOfOneApp);

        }

        private void ScrollRightButton_Click(object sender, RoutedEventArgs e)
        {
            int widthOfOneApp = (int)PresentedApps.First().ActualWidth + 2 * (int)PresentedApps.First().Margin.Left;
            AppsScrollView.ScrollToHorizontalOffset(AppsScrollView.HorizontalOffset + 1 * widthOfOneApp);
        }
    }
}
