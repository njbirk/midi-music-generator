import React from "react";
import { Select } from "grommet";

const Dropdown = ({ name, options, onChange }) => (
  <Select
    name={name}
    options={options.map((option) => option.label)}
    onChange={({ option }) =>
      onChange({
        target: { value: options.find((opt) => opt.label === option).value },
      })
    }
    emptySearchMessage="No options found"
    placeholder="Select an Option"
  />
);

export default Dropdown;
