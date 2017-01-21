import { Component } from '@angular/core';
import { Http } from '@angular/http';
import { NavController, NavParams, LoadingController } from 'ionic-angular';
import { Storage } from '@ionic/storage';
import 'rxjs/add/operator/toPromise';

import { TabsPage } from '../tabs/tabs';

/*
  Generated class for the Login page.

  See http://ionicframework.com/docs/v2/components/#navigation for more info on
  Ionic pages and navigation.
*/
@Component({
  selector: 'page-login',
  templateUrl: 'login.html'
})
export class LoginPage {
  username: string;
  password: string;

  constructor(public navCtrl: NavController,
              public navParams: NavParams,
              public storage: Storage,
              public loadingCtrl: LoadingController,
              public http: Http) {

  }

  ionViewDidLoad() {
    /*
      Si el usuario esta logueado accede a la vista de tabs
      de lo contrario debera iniciar sesion
    */
    this.storage.get('authenticated').then((val) => {
      if (val === true) {
        this.navCtrl.push(TabsPage);
      }
    });
  }


  login(){
    /*
      Mostrar que la aplicacion esta haciendo algo
    */
    let loader =  this.loadingCtrl.create({
      content: "Iniciando sesion...",
      duration: 3000
    });

    loader.present();
    this.http.post('http://localhost:8000/dash/ajax-login/', JSON.stringify({
      "username": this.username,
      "password": this.password
    }))
    .toPromise()
    .then((res) => {
      //let data = res.json();
      this.storage.set('authenticated', true);
      this.navCtrl.push(TabsPage);
      loader.dismiss();
    })
    .catch((err) => {
      //var data = err.json();
      this.storage.set('authenticated', false);
      alert(err);
      loader.dismiss();
    });

  }

}
