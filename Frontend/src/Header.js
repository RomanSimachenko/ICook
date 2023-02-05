import React from "react";
import './Header.css';
import Banner from "./background.png"


class Header extends React.Component {
    constructor() {
        super();
    }

    render() {
        return (
            <header>
                <div className="container-fluid text-center container-bg">
                <img src={Banner} alt="Welcome to ICook" height="50%" width="70%;"/>
            </div>
            </header>
        );
    }
}

export default Header;