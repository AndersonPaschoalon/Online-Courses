using MiscUtil;
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
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
    /// Interação lógica para AnApp.xam
    /// </summary>
    public partial class AnApp : UserControl
    {

        public string AppName;
        public ImageSource AppImageSource;
        public delegate void OnAppClicked(AnApp sender, RoutedEventArgs e);
        public event OnAppClicked AppClicked;


        public AnApp()
        {
            InitializeComponent();
            List<string> filepaths = Directory.GetFiles(Environment.CurrentDirectory + @"\Images\", "*.png").ToList<string>();
            FileInfo myRandomFile = new FileInfo(filepaths[StaticRandom.Next(filepaths.Count)]);
            ProductImage.Source = new BitmapImage(new Uri(myRandomFile.FullName, UriKind.RelativeOrAbsolute));
            AppNameText.Text = (new CultureInfo("en-US", false).TextInfo).ToTitleCase(myRandomFile.FullName.Split('\\').Last().Split('-').Last().Split('.').First());

            AppImageSource = ProductImage.Source;
            AppName = AppNameText.Text.ToString();
        }

        private void ProductImage_MouseUp(object sender, MouseButtonEventArgs e)
        {
            Image senderApp = (System.Windows.Controls.Image)sender;
            Console.WriteLine("Image from App Was Clicked! Now Set the Click event in AnApp too.");
            Console.WriteLine($"---- senderApp (sender):{senderApp.Name}");
            Console.WriteLine($"---- this.Name:{Name}");
            AppClicked(this, e);
        }
    }
}
