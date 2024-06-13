import { createBrowserRouter } from "react-router-dom";
import App from "./App";
import ErrorPage from "./components/error";
import BrowseHomes from "./components/Browse";
import HomeDetails from "./components/HomeDetails";
import SavedHomes from "./components/HomeCard";
import UserProfile from "./components/Profile";
import LandingPage from "./components/Home";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "/",
        element: <LandingPage />,
        index: true,
      },
      {
        path: "/browse",
        element: <BrowseHomes />,
      },
      {
        path: "/homes/:id",
        element: <HomeDetails />,
      },
      {
        path: "/saved",
        element: <SavedHomes />,
      },
      {
        path: "/profile",
        element: <UserProfile />,
      },
    ],
  },
]);

export default router;
