import React from "react";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Select from 'react-dropdown-select';
import dandruffImg from './loopa_for_search.svg'
import './FilterBox.css';

class FilterBox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            categories: [],
            areas: [],
            find_str: '',
            categories_filter: [],
            areas_filter: [],
            products: [],
            amounts: [],
            products_filter: false
        };

        this.sendFilters = this.sendFilters.bind(this);
        this.setFindStr = this.setFindStr.bind(this);
        this.sendSearchQuery = this.sendSearchQuery.bind(this);
        this.setProducts = this.setProducts.bind(this);
    }

    componentDidMount() {
        fetch("http://localhost:8080/api/v1/categories/")
        .then(res => res.json())
        .then(data => {
            this.setState({
                categories: data.categories,
            });
        });

        fetch("http://localhost:8080/api/v1/areas/")
        .then(res => res.json())
        .then(data => {
            this.setState({
                areas: data.areas
            });
        });
    }

    setProducts() {
        if (!this.state.products_filter) {
            let session = sessionStorage.getItem("products");
            this.setState({
                products_filter: true,
                products: session === null ? [] : JSON.parse(session).map(e => e.slug),
                amounts: session === null ? [] : JSON.parse(session).map(e => e.count)
            }, this.sendFilters)
        } else {
            this.setState({
                products_filter: false,
                products: [],
                amounts: []
            }, this.sendFilters);
        }
    }

    sendFilters() {
        let filter = "categories=";
        for (let i = 0; i < this.state.categories_filter.length; i++) {
            const category = this.state.categories_filter[i];
            i == 0 ? filter += category : filter += "," + category;
        }

        filter += ";areas=";

        for (let i = 0; i < this.state.areas_filter.length; i++) {
            const area = this.state.areas_filter[i];
            i == 0 ? filter += area : filter += "," + area;
        }

        filter += ";products=";

        for (let i = 0; i < this.state.products.length; i++) {
            const product = this.state.products[i];
            i == 0 ? filter += product : filter += "," + product;
        }

        filter += ";amounts=";


        for (let i = 0; i < this.state.amounts.length; i++) {
            const amount = this.state.amounts[i];
            i == 0 ? filter += amount : filter += "," + amount;
        }

        filter += ";";

        this.props.body.applyFilters(filter);
    }

    sendSearchQuery() {
        this.props.body.applySearchQuery(this.state.find_str);
    }

    setFindStr(event) {
        this.setState({
            find_str: event.target.value
        });
    }

    preventSubmit(event) {
        event.preventDefault();
    }

    render() {
        return (
            <div className="filter-box">
                <h5 className="text-center" style={{ opacity: 0 }}>Filter by: </h5>
    
                <Form onSubmit={this.preventSubmit} className="d-flex">
                    <Form.Control key={1}
                        type="search"
                        placeholder="Search"
                        className="search-input mr-2"
                        aria-label="Search"
                        onChange={this.setFindStr}/>
                    <Button onClick={this.sendSearchQuery} variant="light" className="search-button">
                        <img src={dandruffImg} alt="Search icon" height="24" width="24"/>
                    </Button>
                </Form>
                {this.props.show_filters ? 
                    <div style={{
                        paddingTop: "20px"
                    }}>

                        <Form.Group>
                            <Select
                                multi
                                options={this.state.categories.map(category => ({value:category.slug,label:category.name})) }
                                placeholder = "Categories..."
                                color="#FFAE6D"
                                onChange={(values) => {
                                                        this.state.categories_filter = values.map(value => value.value);
                                                        this.sendFilters()}
                                        }
                                />
                        </Form.Group>
                        <Form.Group>
                            <Select
                                multi
                                options={this.state.areas.map(area => ({value:area.name,label:area.name})) }
                                placeholder = "Areas..."
                                color="#FFAE6D"
                                onChange={(values) => {
                                    this.state.areas_filter = values.map(value => value.value);
                                    this.sendFilters()}
                                }
                            />
                            </Form.Group>
                            <input onClick={this.setProducts} style={
                                {
                                    marginTop: "20px"
                                }
                            } type="checkbox" value="" id="flexCheckDefault" />
                            <label style={{
                                marginLeft: "5px"
                            }} className="form-check-label" htmlFor="flexCheckDefault">
                                Filter by my products
                            </label>

                    </div>
                    : "" }          </div>
        );
    }
}

export default FilterBox;
