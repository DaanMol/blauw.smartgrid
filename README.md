# blauw.smartgrid
Smart grid project van groep blauw (Thomas Reus, Daan Molleman en Harmke Vliek)

Het smart grid project bestaat uit 150 huizen en 50 batterijen die vastliggen in een grip. In de eerste fase van het project zijn zowel de huizen als de batterijen niet te verplaatsen. Alle huizen hebben een vorm van groene energieopwekking als zonnepanelen of een windmolen. Deze genereren energie dat moet worden opgeslagen wanneer het niet meteen verbruikt wordt. Deze resterende energie wordt middels een verbinding via kabels opgeslagen in een batterij. De kabels worden gelegd volgens de 'Manhattan distance methode'. Alle batterijen hebben een beperkte capaciteit. Het eerste doel van het project is het verbinden van alle huizen aan een batterij zonder de capaciteit van de batterijen te overschrijven. Het tweede doel van het project is de kabels zo neer te leggen dat er een minimum lengte kabels wordt gebruikt. Het derde doel van het project is het minimaliseren van de kabellengte in combinatie met het plaatsen van extra batterijen en het uitzoeken wat meer oplevert, het plaatsen van meer batterijen of het leggen van meer kabels.

In de code worden huizen en batterijen ingeladen waarna deze kunnen worden weergegeven in een plot. Op basis van de x,y coördinaten van zowel de huizen als de batterijen worden deze aan elkaar verbonden. Hierbij worden tevens de kosten van de totale lengte kabels berekend.

Het eerste algoritme dat geprogrammeerd is verbindt alle huizen aan een batterij, zonder de capaciteit van een batterij te overschrijden.
Zodra de capaciteit van de batterij bereikt is worden huizen aan de volgende batterij gekoppeld.
![Algoritme 1](/Presentation/Images/tryout_yfirst_alg0.png)

Het tweede algoritme dat geprogrammeerd is sorteert de huizen zodat de afstanden van een batterij tot een huis van klein naar groot staan.
Vervolgens wordt elk huis aan de dichtstbijzijnde batterij verbonden. Als de capaciteit van de batterij bereikt is worden huizen aan de volgende batterij gekoppeld.
![Algoritme 2](/Presentation/Images/tryout_yfirst.png)

De afbeeldingen zijn gemaakt door gebruik te maken van matplotlib.pylot. 
