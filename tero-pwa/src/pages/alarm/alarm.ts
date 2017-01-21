import { Component } from '@angular/core';
import { Storage } from '@ionic/storage';
import { NavController, NavParams, Platform} from 'ionic-angular';


/*
  Generated class for the Alarm page.

  See http://ionicframework.com/docs/v2/components/#navigation for more info on
  Ionic pages and navigation.
*/
@Component({
  selector: 'page-alarm',
  templateUrl: 'alarm.html'
})
export class AlarmPage {

  constructor(public navCtrl: NavController,
              public navParams: NavParams,
              public storage: Storage,
              public platform: Platform) {}

  ionViewDidLoad() {
    console.log('ionViewDidLoad AlarmPage');
  }

  logout() {
    console.log('salir');
    this.storage.set('authenticated', false);
    this.platform.exitApp();
  }

}
