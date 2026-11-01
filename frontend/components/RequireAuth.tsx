"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { getToken } from "@/lib/auth";

export function RequireAuth({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [autenticado, setAutenticado] = useState<boolean | null>(null);

  useEffect(() => {
    if (getToken()) {
      setAutenticado(true);
    } else {
      setAutenticado(false);
      router.replace("/login");
    }
  }, [router]);

  if (autenticado !== true) {
    // null em vez de um "carregando" visivel: ou autentica rapido, ou redireciona.
    return null;
  }
  return <>{children}</>;
}
