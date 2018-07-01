import React from 'react';

class Page extends React.Component {
 render() {
    console.log( this.props.authUser)
    document.title = "Authorize | DialMail";

    return (
      <div className="container" id="header"style={{marginTop: '70px',marginBottom: '50px'}}>
        <center className="row">
          <div className="col-sm-6 card" style={{margin: 'auto'}}>
            <div className="my-5" style={{color: 'black'}}>
              <h2>DialHut</h2>
                <p>By clicking the button you have grant us authorization to send and recieve emails on your behalf</p>
                <button type="submit" className="btn btn-outline-dark my-3">Accept</button>
            </div>
          </div>
        </center>
      </div>
    );
  }

}

export default Page;
