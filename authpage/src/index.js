import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Page from './component';
import registerServiceWorker from './registerServiceWorker';
import 'bootstrap/dist/css/bootstrap.min.css';

ReactDOM.render(<Page />, document.getElementById('root'));
registerServiceWorker();
