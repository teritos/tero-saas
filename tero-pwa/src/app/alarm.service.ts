import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import { Alarm } from './alarm';
import 'rxjs/add/operator/map';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class AlarmService {

  constructor (private http: Http) {}

  getAlarms(): Observable<Alarm[]> {
    //return this.http.get('http://localhost:8000/api/cliente/?format=json')
    //.map(this.extractData);

    return this.http.get('http://localhost:8000/api/alarm/?format=json')
    .map((res) => res.json());

  }

}
