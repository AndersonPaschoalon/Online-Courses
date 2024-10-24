using InstagramUserControlDemo.Database;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Imaging;

namespace InstagramUserControlDemo.Models
{
    public class PicturePostModel
    {
        public BitmapImage _postImage;

        public BitmapImage PostImage
        {
            get
            {
                if (_postImage == null)
                {
                    _postImage = MockDb.GetPostPicture();
                }
                return _postImage;

            }
            set
            {
                _postImage = value;
            }

        }
    }
}
