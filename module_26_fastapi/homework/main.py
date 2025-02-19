from typing import List, Optional

from fastapi import FastAPI, HTTPException
from sqlalchemy.future import select
from sqlalchemy import update

import models
import schemas
from database import engine, session

# На данную группу импортов нужно заменить предыдущие при запуске
# тестов, иначе тесты не работают
# from . import models
# from . import schemas
# from .database import engine, session


app = FastAPI()


@app.on_event("startup")
async def shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.post('/recipes', response_model=schemas.RecipeIn)
async def create_recipe(recipe: schemas.RecipeIn) -> models.Recipe:
    new_recipe = models.Recipe(**recipe.dict())
    session.add(new_recipe)
    await session.commit()
    await session.refresh(new_recipe)
    return new_recipe


@app.get('/recipes/{idx}', response_model=schemas.RecipeOut)
@app.get('/recipes', response_model=List[schemas.RecipeForBook])
async def recipes(idx: Optional[int] = None) -> schemas.RecipeOut | List[schemas.RecipeForBook]:
    if idx:
        await session.execute(
            update(models.Recipe)
            .where(models.Recipe.id == idx)
            .values(count_views=models.Recipe.count_views + 1)
        )
        await session.commit()

        res = await session.execute(
            select(models.Recipe).where(models.Recipe.id == idx))
        recipe = res.scalar_one_or_none()

        if recipe is None:
            raise HTTPException(status_code=404, detail="Recipe not found")

        return schemas.RecipeOut.from_orm(recipe)

    else:
        await session.execute(
            update(models.Recipe)
            .values(count_views=models.Recipe.count_views + 1)
        )
        await session.commit()

        res = await session.execute(
            select(models.Recipe.dish_name,
                   models.Recipe.count_views,
                   models.Recipe.cooking_time).order_by(models.Recipe.count_views.desc(),
                                                        models.Recipe.cooking_time.asc()))
        recipes = res.all()

        return [schemas.RecipeForBook(dish_name=recipe[0], count_views=recipe[1], cooking_time=recipe[2]) for recipe in
                recipes]
