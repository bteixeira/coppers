SELECT
	sp.date,
	de.description,
	sp.value
FROM
	gastosapp_spending sp,
	gastosapp_spendingtype ty,
	gastosapp_spendingdescription de
where
	sp.type_id = ty.id and
	lower(ty.description) like '%mensal%' and
	sp.description_id = de.id
order by
	sp.date;
