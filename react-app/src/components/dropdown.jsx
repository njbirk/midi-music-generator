import React from "react";
import { Text, Box, Select } from "grommet";

const Dropdown = ({ title, name, options, onChange }) => (
  <Box>
    <Text margin={{ vertical: "small" }} weight="bold">
      {title}
    </Text>
    <Select
      title={title}
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
  </Box>
);

export default Dropdown;
