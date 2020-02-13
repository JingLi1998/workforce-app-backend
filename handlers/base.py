from tornado.web import RequestHandler
from marshmallow.exceptions import ValidationError
from bson.objectid import ObjectId


class BaseHandler(RequestHandler):
    """Configure base handler to perform db query functions."""

    def set_default_headers(self):
        """Allow CORs for development testing."""
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "content-type")
        self.set_header(
            "Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE, PUT, PATCH"
        )

    async def do_find(self, name):
        """Get all document from collection."""
        results = await self.application.templates[name].find().to_list(length=10)
        return [result.dump() for result in results]

    async def do_find_one(self, name, object_id):
        """Get single document from collection."""
        result = await self.application.templates[name].find_one(
            {"_id": ObjectId(object_id)}
        )
        return result.dump()

    async def do_create_one(self, name, req, db_filter):
        """Post new document to collection."""
        if await self.application.templates[name].find_one(db_filter):
            raise ValidationError("Item already exists")
        await self.application.templates[name](**req).commit()

    async def do_update_one(self, name, req, object_id):
        """Put updated document to collection."""
        employee = await self.application.templates[name].find_one(
            {"_id": ObjectId(object_id)}
        )
        employee.update(req)
        await employee.commit()

    async def do_delete_one(self, name, object_id):
        """Delete document from collection."""
        employee = await self.application.templates[name].find_one(
            {"_id": ObjectId(object_id)}
        )
        await employee.delete()

    async def do_create_list_and_reference(self, names, fields, objects):
        """Add list relation and reference relation."""
        object_1 = await self.application.templates[names[0]].find_one(
            {"_id": ObjectId(objects[0])}
        )
        object_2 = await self.application.templates[names[1]].find_one(
            {"_id": ObjectId(objects[1])}
        )
        for object_ref in object_1[fields[0]]:
            if str(object_ref.pk) == objects[1]:
                return
        object_1[fields[0]].append(object_2)
        object_2[fields[1]] = object_1
        await object_1.commit()
        await object_2.commit()

    async def do_create_relation(self, names, fields, objects):
        """Add bi-directional relationship."""
        object_1 = await self.application.templates[names[0]].find_one(
            {"_id": ObjectId(objects[0])}
        )
        object_2 = await self.application.templates[names[1]].find_one(
            {"_id": ObjectId(objects[1])}
        )
        # # add check to prevent duplicates
        for object_ref in object_1[fields[0]]:
            if str(object_ref.pk) == objects[1]:
                return

        for object_ref in object_2[fields[1]]:
            if str(object_ref.pk) == objects[0]:
                return

        object_1[fields[0]].append(object_2)
        object_2[fields[1]].append(object_1)
        await object_1.commit()
        await object_2.commit()

    async def do_populate_one(self, name, object_id, field):
        result = await self.application.templates[name].find_one(
            {"_id": ObjectId(object_id)}
        )
        return (await result[field].fetch()).dump()

    async def do_populate_many(self, name, object_id, field):
        result = await self.application.templates[name].find_one(
            {"_id": ObjectId(object_id)}
        )
        return [(await project.fetch()).dump() for project in result[field]]
