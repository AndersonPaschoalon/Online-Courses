package br.com.andersonp.orgs.extensions
import android.widget.ImageView
import br.com.andersonp.orgs.R
import coil.load


fun ImageView.tryToLoad(url: String? = null){
    load(url){
        fallback(br.com.andersonp.orgs.R.drawable.frutas)
        error(br.com.andersonp.orgs.R.drawable.frutas)
        placeholder(br.com.andersonp.orgs.R.drawable.paceholder)
    }
}
