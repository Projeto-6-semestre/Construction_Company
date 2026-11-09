"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { getToken } from "@/lib/auth";

// Envolve uma pagina do painel interno pra exigir login. Se nao tiver token
// salvo, manda pra /login em vez de mostrar o conteudo protegido (children).
export function RequireAuth({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  // null = ainda nao checou; false = sem token (vai redirecionar); true = pode mostrar a tela.
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
