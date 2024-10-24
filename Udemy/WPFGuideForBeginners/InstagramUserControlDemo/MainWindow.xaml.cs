using InstagramUserControlDemo.Models;
using InstagramUserControlDemo.UserControls;
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

namespace InstagramUserControlDemo
{
    /// <summary>
    /// Interação lógica para MainWindow.xam
    /// </summary>
    public partial class MainWindow : Window
    {
        Random Generator;

        public MainWindow()
        {
            InitializeComponent();

            Generator = new Random(DateTime.Now.Millisecond);

            MainStackPanel.Children.Add(new VideoPostUC(new VideoPostModel()));
            MainStackPanel.Children.Add(new PicturePostUC(new PicturePostModel()));
            MainStackPanel.Children.Add(new VideoPostUC(new VideoPostModel()));
            MainStackPanel.Children.Add(new PicturePostUC(new PicturePostModel()));
        }

        private void MainScrollViewer_ScrollChanged(object sender, ScrollChangedEventArgs e)
        {
            if (e.VerticalChange > 0) 
            {
                int adjustment = 400;
                if (e.VerticalOffset + e.ViewportHeight + adjustment >= e.ExtentHeight) 
                {
                    for (int i = 0; i < 5; i++) 
                    {
                        if (Generator.Next(0, 100) < 70)
                        {
                            PicturePostUC newPost = new PicturePostUC(new PicturePostModel());
                            MainStackPanel.Children.Add(newPost);
                        }
                        else
                        {
                            VideoPostUC newVid = new VideoPostUC(new VideoPostModel());
                            MainStackPanel.Children.Add(newVid);
                        }

                    }
                }
            }
        }
    }
}
