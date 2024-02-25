import { Grommet, Main } from "grommet";
import InputForm from "./components/InputForm";

const theme = {
  global: {
    colors: {
      background: "dark-2",
    },
    font: {
      family: "Roboto",
      size: "18px",
      height: "20px",
    },
  },
};

const App = () => {
  return (
    <Grommet full theme={theme}>
      <Main align="center" justify="evenly">
        <InputForm />
      </Main>
    </Grommet>
  );
};

export default App;
