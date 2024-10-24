using InstagramUserControlDemo.Database;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace InstagramUserControlDemo.Models
{
    public class VideoPostModel
    {

        public Uri _videoPlayersource;

        public Uri VideoPlayerSource 
        {
            get
            {
                if (_videoPlayersource == null)
                {
                    _videoPlayersource = MockDb.GetPostVideo();
                }
                return _videoPlayersource;
                
            }
            set
            {
                _videoPlayersource = value;
            }

        }

    }
}
