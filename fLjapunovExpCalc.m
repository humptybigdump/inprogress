function [vT,xLambda,vT_ges,vX_ges] = fLjapunovExpCalc(fODE,vParams, fSolver, log, sODE_options,vX0,nT0,nT1,nT_f);
  %% Beschreibung
  % Programmiert nach Nayfeh, Balachandran - "Applied Nonlinear Dynamics",
  % Kapitel 7. Validiert für Nayfeh-Ergebnisse zum Rössler- und Lorenzattraktor. 
  % Die Ljapunov-Exponenten werden mit dem Gram-Schmidt-Verfahren zur
  % Orthogonalisierung der Störungen im System berechnet
  
  %% Initialisierung
  nN      = size(vX0,1);   % Dimension der DGL
  vT_ges  = [];
  vX_ges  = [];
  nR      = round((nT1-nT0)/nT_f);
  xY      = eye(nN);
  vX0_i   = vX0;
  nT0_i   = nT0;
  nT1_i   = nT0 + nT_f;
  xN_ij   = zeros(nR,nN);
  xLambda = NaN(nR,nN);
  vT      = (1:nR)*nT_f;
  
  %% Zeitintegration: 
  for nI = 1:nR
    % Integration mit Abweichungen y_i (alle y_i Gleichzeitig in Matrix xY)
    [vT_i,vX_i] = feval(fSolver, @(t,x) fODE(t,x,vParams), [nT0_i nT1_i], [vX0_i;xY(:)], sODE_options);
    vT_ges = [vT_ges;vT_i];
    vX_ges = [vX_ges;vX_i(:,1:nN)];
    xY_i = reshape(vX_i(end,nN+1:end),nN,nN);
    % Gram-Schmidt-Verfahren (Orthogonalisierung der Vektoren)
    xY_GSV(:,1) = xY_i(:,1)/norm(xY_i(:,1));
    xN_ij(nI,1) = norm(xY_i(:,1));
    for nJ = 2:nN
      vY_proj = zeros(size(vX0_i));
      for nK = 1:nJ-1
        vY_proj = vY_proj + (xY_i(:,nJ).'*xY_GSV(:,nK))*xY_GSV(:,nK);
      end
      xY_GSV(:,nJ) = (xY_i(:,nJ)-vY_proj)/norm(xY_i(:,nJ)-vY_proj);
      xN_ij(nI,nJ) = norm(xY_i(:,nJ)-vY_proj);
    end
    % Berechnung der Ljapunov exponenten zum Zeitpunkt nR*nDelta_T
    xLambda(nI,:) = 1/(nI*nT_f)*sum(log(xN_ij(1:nI,:)),1);
    % Vorbereitung für nächsten Schritt
    nT0_i = nT1_i;
    nT1_i = nT1_i + nT_f;
    vX0_i = vX_ges(end,:).';
    xY    = xY_GSV;
  end 
end
