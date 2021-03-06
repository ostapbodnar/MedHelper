import React from "react";
import { Link } from "react-router-dom";

export function AddButton(props) {
  return (
    <>
      <Link
        to={props.to}
        className={`btn-success ${props.className} btn mx-auto mt-auto mb-4 child-center`}
      >
        {props.children}
      </Link>
    </>
  );
}
