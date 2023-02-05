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
            areas_filter: []
        };

        this.sendFilters = this.sendFilters.bind(this);
        this.setFindStr = this.setFindStr.bind(this);
        this.sendSearchQuery = this.sendSearchQuery.bind(this);
        this.addCategory = this.addCategory.bind(this);
        this.addArea = this.addArea.bind(this);
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

    addCategory(event) {
        if (this.state.categories_filter.indexOf(event.target.value) === -1) {
            this.setState({
                categories_filter: [...this.state.categories_filter, event.target.value]
            }, this.sendFilters);
        } else {
            this.setState({
                categories_filter: this.state.categories_filter.filter(e => e != event.target.value)
            }, this.sendFilters);
        }
    }

    addArea(event) {
        console.log(event.target.value);
        if (this.state.areas_filter.indexOf(event.target.value) === -1) {
            this.setState({
                areas_filter: [...this.state.areas_filter, event.target.value]
            }, this.sendFilters);
        } else {
            this.setState({
                areas_filter: this.state.areas_filter.filter(e => e != event.target.value)
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

    render() {
        return (
            <div className="filter-box">
                <h5 className="text-center" style={{ opacity: 0 }}>Filter by: </h5>
    
                <Form className="d-flex">
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
                <div>

                    <Form.Group>
                        <Select
                            multi
                            options={this.state.categories.map(category => ({value:category.slug,label:category.name})) }
                            placeholder = "Categories..."
                            color="#FFAE6D"
                            />
                    </Form.Group>
                    <Form.Group>
                        <Select
                            multi
                            options={this.state.areas.map(area => ({value:area.id,label:area.name})) }
                            placeholder = "Areas..."
                            color="#FFAE6D"
                        />
                    </Form.Group>
                </div> 
            : 
            <div></div>}
    
            </div>
        );
    }
}

/*const FilterBox = (props) => {
    const { receipts } = props;

    const categories = [...new Set(receipts.map(receipt => receipt.strCategory))];
    const areas = [...new Set(receipts.map(receipt => receipt.strArea))];

   

};*/


export default FilterBox;
