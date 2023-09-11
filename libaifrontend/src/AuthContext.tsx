// AuthContext.tsx
import React, {
  createContext,
  useState,
  useEffect,
  ReactNode,
  useContext,
} from "react";
import { redirect } from "react-router-dom";
import apios from "./apios";
import { UserOut, UserOutToken } from "./api";
import { AxiosResponse } from "axios";

type AuthContextType = {
  user: UserOut | null;
  setUser: (user: UserOut | null) => void;
  userLoading: boolean;
  login: (token: string) => void; // updated to accept token
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<UserOut | null>(null);
  const [userLoading, setUserLoading] = useState<boolean>(true);

  useEffect(() => {
    const token = localStorage.getItem("jwt_token");
    if (token) {
      apios.get("/u/me")
        .then((resp: AxiosResponse) => {
          setUser(resp.data);
        })
        .catch((error) => {
            if (error.response.status === 401) {
                // token is invalid
                localStorage.removeItem("jwt_token");
            }
            console.error(error);
        })
        .finally(() => {
          setUserLoading(false);
        });
    } else {
      setUserLoading(false);
    }
  }, []);

  const login = (token: string) => {
    localStorage.setItem("jwt_token", token); // storing token on successful login
  };

  const logout = () => {
    localStorage.removeItem("jwt_token");

  };

  return (
    <AuthContext.Provider value={{ user, setUser, userLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
