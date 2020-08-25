import { Application } from 'stimulus';
import { definitionsFromContext } from 'stimulus/webpack-helpers';
import React, { Component } from 'react';
import Turbolinks from 'turbolinks';
import ReactDOM from 'react-dom';


import StimulusReflex from 'stimulus_reflex'
import WebsocketConsumer from 'sockpuppet-js'
import IndexController from './controllers/index_controller'


const application = Application.start();
Turbolinks.start();

const consumer = new WebsocketConsumer('ws://127.0.0.1:8000/ws/sockpuppet-sync')

application.register("index", IndexController)
StimulusReflex.initialize(application, { consumer })

class App extends React.Component {
  render() {
    return (
      <div>
        <h1>Hello these are my notes</h1>
      </div>
    );
  }
}

ReactDOM.render(<App />, document.getElementById('react-app'));
