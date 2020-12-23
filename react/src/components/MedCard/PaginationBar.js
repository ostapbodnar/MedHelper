import React from "react";
import Pagination from "react-bootstrap/Pagination";

function range(start, stop, step = 1) {
  var a = [];
  for (let i = start; i < stop; i += step) {
    a.push(i);
  }
  return a;
}

export class PaginationBar extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      current: props.current,
      number_of_pages: props.number,
      objects: this.getObjects(props.number, props.current),
    };
  }

  componentDidUpdate() {
    if (this.props.number != this.state.number_of_pages) {
      this.setState({
        number_of_pages: this.props.number,
        objects: this.getObjects(this.props.number, this.state.current),
      });
    }
  }

  getObjects = (number, current) => {
    var number_of_pages = number;
    if (number_of_pages < 7) {
      var ranges = range(1, number_of_pages + 1);
    } else {
      var current = current;

      var ranges =
        current - 3 < 1
          ? range(1, 7)
          : current + 3 > number_of_pages
          ? range(number_of_pages - 5, number_of_pages + 1)
          : range(current - 2, current + 3);
    }

    ranges = [...new Set(ranges).values()].sort();

    var objs = [];
    if (ranges[0] != 1) {
      objs.push(<Pagination.Ellipsis key={101} />);
    }
    for (let i = 0; i < ranges.length; i++) {
      objs.push(
        <Pagination.Item
          key={i}
          onClick={() => this.handleClick(ranges[i])}
          active={current == ranges[i]}
        >
          {ranges[i]}
        </Pagination.Item>
      );
    }
    if (ranges[ranges.length - 1] != number_of_pages) {
      objs.push(<Pagination.Ellipsis key={102} />);
    }
    return objs;
  };

  handleClick = (new_curr) => {
    if (new_curr > 0 && new_curr <= this.state.number_of_pages) {
      this.setState(
        {
          ...this.state,
          current: new_curr,
          objects: this.getObjects(this.state.number_of_pages, new_curr),
        },
        () => {
          this.props.onClick(this.state.current);
        }
      );
    }
  };

  render() {
    return (
      <Pagination className={`${this.props.className}`}>
        <Pagination.First
          onClick={() => {
            this.handleClick(1);
          }}
        />
        <Pagination.Prev
          onClick={() => {
            this.handleClick(this.state.current - 1);
          }}
        />

        {this.state.objects.map((elem) => {
          return elem;
        })}

        <Pagination.Next
          onClick={() => {
            this.handleClick(this.state.current + 1);
          }}
        />
        <Pagination.Last
          onClick={() => {
            this.handleClick(this.state.number_of_pages);
          }}
        />
      </Pagination>
    );
  }
}
