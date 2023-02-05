import React from "react";
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import './NavBar.css'
import logo from './logo_image.svg';


class NavBar extends React.Component {
  constructor() {
    super();
  }

  render() {
    return (

        <Navbar expand="md" sticky="top" >
            <Navbar.Brand href="/"><img src={logo} alt="Logo" width="auto" height="50vw"/></Navbar.Brand>
            <Navbar.Brand href="/" className="ICookText">ICook</Navbar.Brand>

            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav" className="position-relative">
                <Nav className="position-absolute end-0">
                    <Nav.Link className="btn-NavBar mx-2 top-50" href="/">Receipts</Nav.Link>
                    <Nav.Link className="btn-NavBar mx-2 top-50" href="/products">Products</Nav.Link>
                    <Nav.Link className="btn-NavBar mx-2" href="/products">
                        <i className="bi-cart-fill me-1"></i>
                        CART
                        <span className="badge bg-white text-white ms-1 rounded-pill">
                                      <span style={{
                                          color: "black"
                                      }}>{sessionStorage.getItem("products_count") == null ? 0 : sessionStorage.getItem("products_count")}</span>
                                    </span>
                    </Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    );
  }
}

export default NavBar;
