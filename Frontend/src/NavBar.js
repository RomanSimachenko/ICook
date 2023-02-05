import React from "react";
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import './NavBar.css'
import logo from './logo_image.svg';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

const PRODUCTS_THUMB_URL = "http://localhost:8080/media/products/";

class NavBar extends React.Component {
  constructor() {
    super();
    this.state = {
      modalOpen: false
    }
    this.openModal = this.openModal.bind(this);
    this.closeModal = this.closeModal.bind(this);
  }

  openModal() {
      this.setState({
        modalOpen: true
      });
  }

  closeModal() {
      this.setState({
        modalOpen: false
      });
  }

  render() {
    return (
      <div>
        <Navbar expand="md" sticky="top" >
            <Navbar.Brand href="/"><img src={logo} alt="Logo" width="auto" height="50vw"/></Navbar.Brand>
            <Navbar.Brand href="/" className="ICookText">ICook</Navbar.Brand>

            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav" className="position-relative">
                <Nav className="position-absolute end-0">
                    <Nav.Link className="btn-NavBar mx-2 top-50" href="/">Receipts</Nav.Link>
                    <Nav.Link className="btn-NavBar mx-2 top-50" href="/products">Products</Nav.Link>
                    <Nav.Link onClick={this.openModal} className="btn-NavBar mx-2" href="">
                        <i className="bi-cart-fill me-1"></i>
                        CART
                        <span className="badge bg-white text-white ms-1 rounded-pill">
                        </span>
                    </Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
        <Dialog
        open={this.state.modalOpen}
        keepMounted
        onClose={this.closeModal}
        aria-describedby="alert-dialog-slide-description"
      >
        <DialogTitle>{"Your products: "}</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-slide-description">
          {sessionStorage.getItem("products") !== null ? JSON.parse(sessionStorage.getItem("products")).map((product, index) => {
                          return (
                              <div key={index} className="container-fluid">
                                  <div className="row">
                                      <div className="col-12 mt-3">
                                          <div className="card">
                                              <div className="card-horizontal">
                                                  <div className="img-square-wrapper">
                                                      <img className="" src={PRODUCTS_THUMB_URL + product.slug + "-small.png"} alt="Card image cap"/>
                                                  </div>
                                                  <div className="card-body">
                                                      <h4 className="card-title">{product.name}</h4>
                                                      <p className="card-text">You have: {product.count}</p>
                                                  </div>
                                              </div>
                                          </div>
                                      </div>
                                  </div>
                              </div>
                          );
                    }) : "You have no products in the cart!"}
          </DialogContentText>
        </DialogContent>
      </Dialog>
      </div>
    );
  }
}

export default NavBar;