import React from "react";
import {BrowserRouter, Routes, Route} from "react-router-dom";
import NavBar from "./NavBar";
import Header from "./Header";
import Body from "./Body";
import ProductsBody from "./ProductsBody";
import Receipt from "./Receipt";
class App extends React.Component {
    constructor() {
        super();
    }

    render() {
        return (
            <BrowserRouter>
            <Routes>
              <Route path="/" element={
                <div>
                    <NavBar />
                    <Header />
                    <Body />
                </div>
                }>
              </Route>
              <Route path="/products" element={
                  <div>
                      <NavBar />
                      <Header />
                      <ProductsBody />
                  </div>
              }>
              </Route>
              <Route path="/receipt/:receipt" element={
                <div>
                    <NavBar />
                    <br />
                    <Receipt />
                </div>
              }>
              </Route>
            </Routes>
          </BrowserRouter>
        );
    }
}

export default App;