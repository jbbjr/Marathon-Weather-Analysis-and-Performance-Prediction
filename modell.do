clear
local path = "file"
import delimited using `path'
ssc install reghdfe

// null replaced with zero, as these variables sometimes show up as null when they do not happen
replace snowdepth0_6 = 0 if snowdepth0_6 == .
replace snowdepth6_12 = 0 if snowdepth6_12 == .
replace snowdepth12_18 = 0 if snowdepth12_18 == .
replace snowdepth18_24 = 0 if snowdepth18_24 == .

replace cloudcover0_6 = 0 if cloudcover0_6 == .
replace cloudcover6_12 = 0 if cloudcover6_12 == .
replace cloudcover12_18 = 0 if cloudcover12_18 == .
replace cloudcover18_24 = 0 if cloudcover18_24 == .

// time to seconds
split time, parse(":")
destring(time1), replace
destring(time2), replace
destring(time3), replace
gen seconds = (time1*3600) + (time1*60) + time3
drop time1
drop time2
drop time3

egen high = rowmax(high0_6 high6_12 high12_18 high18_24)
egen low = rowmin(low0_6 low6_12 low12_18 low18_24)

drop high0_6
drop high6_12 
drop high12_18
drop high18_24
drop low0_6
drop low6_12
drop low12_18
drop low18_24


destring(divplace), replace


// exploratory stuff
egen raceID = group(race)
egen avgtemp = rowmean(temp0_6 temp6_12 temp12_18 temp18_24)
save unbalPanelRaces.dta, replace


duplicates drop racekey, force
egen variance = sd(avgtemp), by(raceID)
replace variance = variance * variance
keep variance racekey raceID

save raceVariance.dta, replace

clear
use unbalPanelRaces.dta
merge m:1 racekey using raceVariance.dta
drop _merge
erase raceVariance.dta

gsort -variance


gen datetime = date + " " + time

save temp.dta, replace

// name
drop if strpos(name, ",") > 0

split name, parse("(F)" "(F1" "(F2" "(F3" "(F4" "(F5" "(F6" "(F7" "(F8" "(F9" "(M)" "(M1" "(M2" "(M3" "(M4" "(M5" "(M6" "(M7" "(M8" "(M9" ) generate(nametest)

rename nametest1 runnername
replace runnername = trim(runnername)
drop nametest2

// gender
gen tempvar = strrpos(name, "(") + 1
gen sex = substr(name,tempvar,1)
drop tempvar
replace sex = "" if sex~="M" & sex~="F"

// age
gen age = substr(name,-3,2)
replace age = "" if strpos(age, "(") > 0 | strpos(age, "M") > 0 | strpos(age, "F") > 0

drop if age == ""
destring(age), replace
gen isMale = 1 if sex == "M"
replace isMale = 0 if isMale == .
drop if sex == ""

// Quadratic term for temp
gen temp6_12sq = temp6_12 * temp6_12

// OLS
reg seconds age isMale temp6_12sq overall divplace sexplace temp0_6 temp6_12 temp12_18 temp18_24 dew0_6 dew6_12 dew12_18 dew18_24 humidity0_6 humidity6_12 humidity12_18 humidity18_24 windspeed0_6 windspeed6_12 windspeed12_18 windspeed18_24 precipitation0_6 precipitation6_12 precipitation12_18 precipitation18_24 snowdepth0_6 snowdepth6_12 snowdepth12_18 snowdepth18_24 cloudcover0_6 cloudcover6_12 cloudcover12_18 cloudcover18_24

// fixed effect for race
reghdfe seconds age isMale temp6_12sq overall divplace sexplace temp0_6 temp6_12 temp12_18 temp18_24 dew0_6 dew6_12 dew12_18 dew18_24 humidity0_6 humidity6_12 humidity12_18 humidity18_24 windspeed0_6 windspeed6_12 windspeed12_18 windspeed18_24 precipitation0_6 precipitation6_12 precipitation12_18 precipitation18_24 snowdepth0_6 snowdepth6_12 snowdepth12_18 snowdepth18_24 cloudcover0_6 cloudcover6_12 cloudcover12_18 cloudcover18_24, absorb(raceID)

// fix for runner
egen namecount = count(runnername), by(runnername)
replace runnername = lower(runnername)
drop if namecount < 2
drop if namecount > 60
drop if strmatch(runnername, "*unknown*")

// in same race
gen tempkey = runnername + "_" + string(age) + "_" + sex + race + string(year)
replace tempkey = lower(tempkey)
egen same = count(tempkey), by(tempkey)
drop if same > 1
egen runnerID = group(runnername)

// runner and race 
reghdfe seconds age isMale temp6_12sq overall divplace sexplace temp0_6 temp6_12 temp12_18 temp18_24 dew0_6 dew6_12 dew12_18 dew18_24 humidity0_6 humidity6_12 humidity12_18 humidity18_24 windspeed0_6 windspeed6_12 windspeed12_18 windspeed18_24 precipitation0_6 precipitation6_12 precipitation12_18 precipitation18_24 snowdepth0_6 snowdepth6_12 snowdepth12_18 snowdepth18_24 cloudcover0_6 cloudcover6_12 cloudcover12_18 cloudcover18_24, absorb(raceID runnerID)

// runner and race and time
reghdfe seconds age isMale temp6_12sq overall divplace sexplace temp0_6 temp6_12 temp12_18 temp18_24 dew0_6 dew6_12 dew12_18 dew18_24 humidity0_6 humidity6_12 humidity12_18 humidity18_24 windspeed0_6 windspeed6_12 windspeed12_18 windspeed18_24 precipitation0_6 precipitation6_12 precipitation12_18 precipitation18_24 snowdepth0_6 snowdepth6_12 snowdepth12_18 snowdepth18_24 cloudcover0_6 cloudcover6_12 cloudcover12_18 cloudcover18_24, absorb(raceID runnerID year)

erase temp.dta

